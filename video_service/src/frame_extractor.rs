use std::env;
use opencv::{
    prelude::*,
    Result,
};
use opencv;
use opencv::core::Vector;
use opencv::videoio::{CAP_ANY, VideoCaptureTrait};

pub unsafe fn extract_frames(file: &str) -> Result<Vector<String>, String> {
    let dir_res = env::var("OUTPUT_DIR");
    if dir_res.is_err() {
        return Err("Failed to get dir for extracted files".to_string());
    }
    let dir = dir_res.unwrap();
    let dir_create_res = std::fs::create_dir_all(&dir);
    if dir_create_res.is_err() {
        error!("Failed to create dir for output files. Err: {:?}", dir_create_res.err());
        return Err("Failed to create dir for output files.".to_string());
    }

    info!("Extracting frames from: {}", file);
    let video_res = opencv::videoio::VideoCapture::from_file(file, CAP_ANY);
    if video_res.is_err() {
        error!("Failed to get videoCapture. Err: {:?}", video_res.err());
        return Err("Failed to get videoCapture".to_string());
    }

    let mut frame = Mat::default();
    let mut video = video_res.unwrap();
    let read_res = video.read(&mut frame);
    if read_res.is_err() {
        error!("Failed to read frame. Err: {:?}", read_res.err());
        return Err("Failed to read frame".to_string());
    }

    info!("Extracting frames to dir: {}", dir);
    let mut frame_count = 0;
    let mut extracted_frame_count = 0;
    let mut seconds_in_movie = 0;
    let mut working = read_res.unwrap();
    let mut files_list = Vector::<String>::new();
    if !working {
        error!("Can not extract frames.");
        return Err("Can not extract frames.".to_string());
    }
    while working {
        if frame_count % 100 == 0 {
            seconds_in_movie = frame_count / 30;
            let filename = format!("{}-second-{}.jpg", dir, seconds_in_movie);
            let mut params = opencv::core::Vector::new();
            opencv::imgcodecs::imwrite(&filename, &frame, &params);
            files_list.push(filename.as_str());

            extracted_frame_count = extracted_frame_count + 1;
        }
        let next_read_res = video.read(&mut frame);
        if next_read_res.is_err() {
            return Err("Failed to read frame".to_string());
        }
        frame_count = frame_count + 1;
        working = next_read_res.unwrap();
    }
    info!("List of files with frames {:?}", files_list);
    info!("Extracted {} frames", extracted_frame_count);
    return Ok(files_list);
}