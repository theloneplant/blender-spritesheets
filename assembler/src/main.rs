use image::RgbaImage;
use std::cmp::max;
use std::path::PathBuf;

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
        .arg(
            clap::Arg::with_name("output")
                .short("o")
                .long("out")
                .value_name("PNG_FILENAME")
                .help("Spritesheet output filename")
                .takes_value(true),
        )
        .get_matches();

    let root = matches.value_of("root").unwrap();
    let images = collect_images(root);
    let dims = dims(&images)?;
    let tiles = optimal_stacking(images.len(), dims);
    let max_axis = {
        let width = tiles.x * dims.x;
        let height = tiles.y * dims.y;
        max(width, height)
    };

    let mut out: RgbaImage = image::ImageBuffer::new(max_axis as u32, max_axis as u32);
    for (i, img) in images.iter().enumerate() {
        let x = (i % tiles.x) * dims.x;
        let y = (i / tiles.x) * dims.y;
        image::imageops::replace(&mut out, img, x as u32, y as u32);
    }

    let output = matches.value_of("output").unwrap_or("out.png");
    let out_path: PathBuf = [root, output].iter().collect();
    out.save(out_path)
        .map_err(|_| "Failed to save spritesheet")?;

    Ok(())
}

fn dims(images: &[RgbaImage]) -> Result<Dims, &'static str> {
    let mut iter = images.iter();
    let first = match iter.next() {
        Some(first) => Ok(first),
        _ => Err("Should have found at least one image"),
    }?;
    let dims = first.dimensions();
    if images.iter().all(|next| next.dimensions() == dims) {
        Ok(Dims {
            x: dims.0 as usize,
            y: dims.1 as usize,
        })
    } else {
        Err("All images should have the same format")
    }
}

fn optimal_stacking(count: usize, dims: Dims) -> Dims {
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
            let dim = max(y * dims.y, x * dims.x);
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

fn collect_images(root: &str) -> Vec<RgbaImage> {
    let temporary: PathBuf = [root, "temp"].iter().collect();
    walkdir::WalkDir::new(temporary)
        .sort_by(|a, b| a.file_name().cmp(b.file_name()))
        .into_iter()
        .filter_map(|e| match image_filter(e) {
            Ok(img) => Some(img),
            Err(_) => None,
        })
        .collect::<Vec<_>>()
}

fn image_filter(entry: Result<walkdir::DirEntry, walkdir::Error>) -> Result<RgbaImage, ()> {
    match image::open(entry.map_err(|_| ())?.path()).map_err(|_| ())? {
        image::ImageRgba8(img) => Ok(img),
        _ => Err(()),
    }
}
