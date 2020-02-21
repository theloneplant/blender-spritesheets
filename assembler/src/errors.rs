use std::{error, fmt};

#[derive(Debug, Clone)]
pub struct ImageFormatError;

impl fmt::Display for ImageFormatError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Images should be 8-bit RGBA")
    }
}

impl error::Error for ImageFormatError {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        None
    }
}

#[derive(Debug, Clone)]
pub struct InconsistentSizeError;

impl fmt::Display for InconsistentSizeError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Images should all be the same size")
    }
}

impl error::Error for InconsistentSizeError {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        None
    }
}

#[derive(Debug, Clone)]
pub struct NoImagesError;

impl fmt::Display for NoImagesError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "No images found")
    }
}

impl error::Error for NoImagesError {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        None
    }
}
