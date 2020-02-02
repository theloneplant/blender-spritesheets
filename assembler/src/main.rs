#[derive(Debug, Copy, Clone)]
struct Dims {
    x: usize,
    y: usize,
}

fn main() -> Result<(), &'static str> {
    let matches = clap::App::new("assembler")
        .about("Combined PNGs into a spritesheet")
        .arg(
            clap::Arg::with_name("root")
                .short("r")
                .long("root")
                .value_name("DIR")
                .help("Where to search for spritesheet tiles")
                .takes_value(true)
                .required(true),
        )
        .get_matches();

    let root = matches.value_of("root").unwrap();

    let images = collect_images(root);

    match images.len() {
        0 => Err("Should have found at least one image"),
        _ => Ok(()),
    }?;

    let dims = dims(&images)?;
    let tiles = optimal_stacking_width(images.len(), dims);

    let width = tiles.x * dims.x;
    let height = tiles.y * dims.y;
    let max_axis = std::cmp::max(width, height);

    let mut out: image::RgbaImage = image::ImageBuffer::new(max_axis as u32, max_axis as u32);
    for i in 0..images.len() {
        let x = (i % tiles.x) * dims.x;
        let y = (i / tiles.x) * dims.y;
        image::imageops::replace(&mut out, &images[i], x as u32, y as u32);
    }

    let out_path: std::path::PathBuf = [root, "out.png"].iter().collect();
    out.save(out_path)
        .map_err(|_| "Could not save spritesheet")?;

    Ok(())
}

fn dims(images: &[image::RgbaImage]) -> Result<Dims, &'static str> {
    let mut iter = images.iter();
    let first = iter.next().unwrap();
    let dims = first.dimensions();
    match images
        .iter()
        .fold(true, |acc, next| acc && next.dimensions() == dims)
    {
        true => Ok(Dims {
            x: dims.0 as usize,
            y: dims.1 as usize,
        }),
        false => Err("All images should have the same format"),
    }
}

fn optimal_stacking_width(count: usize, dims: Dims) -> Dims {
    struct Min {
        dim: usize,
        x: usize,
    }
    let Min { x, .. } = (1..=count).fold(
        Min {
            dim: std::usize::MAX,
            x: 0,
        },
        |min, x| {
            let y = y_from_x(x, count);
            let dim = std::cmp::max(y * dims.y, x * dims.x);
            if dim < min.dim {
                Min { x, dim }
            } else {
                min
            }
        },
    );
    Dims {
        x,
        y: y_from_x(x, count),
    }
}

fn y_from_x(x: usize, count: usize) -> usize {
    (count as f32 / x as f32).ceil() as usize
}

fn collect_images(root: &str) -> Vec<image::RgbaImage> {
    let temporary: std::path::PathBuf = [root, "temp"].iter().collect();
    walkdir::WalkDir::new(temporary)
        .into_iter()
        .filter_map(|e| match image_filter(e) {
            Ok(img) => Some(img),
            Err(_) => None,
        })
        .collect::<Vec<_>>()
}

fn image_filter(entry: Result<walkdir::DirEntry, walkdir::Error>) -> Result<image::RgbaImage, ()> {
    match image::open(entry.map_err(|_| ())?.path()).map_err(|_| ())? {
        image::ImageRgba8(img) => Ok(img),
        _ => Err(()),
    }
}
