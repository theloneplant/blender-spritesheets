fn main() -> Result<(), &'static str> {
    let matches = clap::App::new("assembler")
        .about("Combined PNGs into a spritesheet")
        .arg(
            clap::Arg::with_name("root")
                .short("r")
                .long("root")
                .value_name("DIR")
                .help("Where to search for spritesheet tiles")
                .takes_value(true),
        )
        .get_matches();

    let root = match matches.value_of("root") {
        Some(root) => root.into(),
        None => std::env::current_dir().map_err(|_| "Could not get pwd")?,
    };

    let images = collect_images(root);

    match images.len() {
        0 => Err("Should have found at least one image"),
        _ => Ok(()),
    }?;

    let dims = dims(&images)?;
    let across = optimal_stacking_width(&images, dims);

    Ok(())
}

fn dims(images: &[image::RgbaImage]) -> Result<(usize, usize), &'static str> {
    let mut iter = images.iter();
    let first = iter.next().unwrap();
    let dims = first.dimensions();
    match images
        .iter()
        .fold(true, |acc, next| acc && next.dimensions() == dims)
    {
        true => Ok((dims.0 as usize, dims.1 as usize)),
        false => Err("All images should have the same format"),
    }
}

fn optimal_stacking_width(images: &[image::RgbaImage], dims: (usize, usize)) -> usize {
    struct Min {
        area: usize,
        y: usize,
    }
    let Min { y, .. } = (1..images.len() - 1).fold(
        Min {
            area: std::usize::MAX,
            y: 0,
        },
        |acc, y| {
            let x = images.len() / y + images.len() % y;
            let area = y * dims.0 + x * dims.1;
            if area < acc.area {
                Min { y, area }
            } else {
                acc
            }
        },
    );
    images.len() / y + images.len() % y
}

fn collect_images(root: std::path::PathBuf) -> Vec<image::RgbaImage> {
    walkdir::WalkDir::new(root)
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
