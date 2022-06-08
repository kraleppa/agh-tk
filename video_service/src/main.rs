use std::{env, thread, time};
use amiquip::{Channel, Connection, ConsumerMessage, ConsumerOptions, Publish, Result};
use log::LevelFilter;
use opencv::core::Vector;

#[macro_use]
extern crate log;
extern crate env_logger;

pub mod frame_extractor;

use serde_json::{Map, Value};

fn main() -> Result<()> {
    env_logger::builder()
        .filter_level(LevelFilter::Info)
        .init();
    info!("Prepering conncection");
    let rabit_connection_res = env::var("RABBIT_CONNECTION_STRING");
    if rabit_connection_res.is_err() {
        return Ok(());
    }

    let rabit_connection = rabit_connection_res.unwrap();
    info!("Rabbit connection: {}", rabit_connection);

    let mut connection_res = Connection::insecure_open(&rabit_connection);

    let three_sec = time::Duration::from_secs(3);
    while connection_res.is_err() {
        info!("Trying to connect to rabbitmq");
        thread::sleep(three_sec);
        connection_res = Connection::insecure_open(&rabit_connection);
    }
    info!("Connected to rabbitmq");
    let mut connection = connection_res.unwrap();
    let channel = connection.open_channel(None)?;

    let consumer = channel.basic_consume("format.movie", ConsumerOptions::default())?;

    info!("Consumer loop starting");
    for (_, message) in consumer.receiver().iter().enumerate() {
        match message {
            ConsumerMessage::Delivery(delivery) => unsafe {
                let mut file_error = false;
                let body = String::from_utf8_lossy(&delivery.body);
                let res = serde_json::from_str(&body);
                if res.is_err() {
                    error!("Received invalid msg: {:?}", res.err());
                    consumer.ack(delivery)?;
                    continue;
                }
                let v: Value = res.unwrap();
                let file_option = v["file"].as_str();
                if file_option.is_none() {
                    error!("Message does not contain file property");
                    file_error = true;
                    send_json_without_frames(&channel, &v, file_error);
                    consumer.ack(delivery)?;
                    continue;
                }

                let file = file_option.unwrap();
                info!("file: {}", file);
                let result_files_with_frames = frame_extractor::extract_frames(file);
                if result_files_with_frames.is_err() {
                    error!("no frames extracted {:?}", result_files_with_frames.err());
                    file_error = true;
                    send_json_without_frames(&channel, &v, file_error);
                    consumer.ack(delivery)?;
                    continue;
                }

                let files_with_frames = result_files_with_frames.unwrap();
                send_json_with_frames(&channel, &files_with_frames, &v);
                consumer.ack(delivery)?;
            }
            other => {
                info!("Consumer ended: {:?}", other);
                break;
            }
        }
    }

    info!("Consumer loop finished");
    connection.close()
}

fn send_json_with_frames(channel: &Channel, files_with_frames: &Vector<String>, value: &Value) {
    for file in files_with_frames.iter() {
        let mut to_send = value.clone();
        let mut map = Map::new();
        map.insert("filePathInVolume".to_string(), Value::String(file));
        map.insert("numberOfExtractedFrames".to_string(),Value::from(files_with_frames.capacity()));
        to_send["video"] = Value::Object(map);
        let mut fileStateJson = &mut to_send["fileState"];
        if fileStateJson.is_object() {
            let mut fileStateJsonObject = fileStateJson.as_object_mut().unwrap();
            fileStateJsonObject.insert("fileProcessed".to_string(), Value::from(true));
            fileStateJsonObject.insert("fileProcessingError".to_string(), Value::from(false));
        }
        //to_send["extractionSource"] = Value::String("video".to_string());

        let mut msg_to_send = to_send.to_string();
        info!("Sending to scraper: {}", msg_to_send);
        channel.basic_publish("words", Publish::new(msg_to_send.as_bytes(), "words.scraper"));

        info!("Sending to result: {}", msg_to_send);
        channel.basic_publish("result", Publish::new(msg_to_send.as_bytes(), "result"));
    }
}

fn send_json_without_frames(channel: &Channel, value: &Value, file_error: bool) {
    let mut to_send = value.clone();
    let mut fileStateJson = &mut to_send["fileState"];
    if fileStateJson.is_object() {
        let mut test = fileStateJson.as_object_mut().unwrap();
        if file_error {
            test.insert("fileProcessingError".to_string(), Value::from(file_error));
        }
    }
    let mut msg_to_send = to_send.to_string();
    info!("Sending to result: {}", msg_to_send);
    channel.basic_publish("result", Publish::new(msg_to_send.as_bytes(), "result"));
}

#[cfg(test)]
mod extractor_test {
    use std::path::{PathBuf};
    use crate::frame_extractor;

    #[test]
    #[should_panic]
    fn failed_extract() {
        let file = PathBuf::from("/non/existing/path/test.mp4");
        let file_path = file.to_str().unwrap();
        let result_files_with_frames = unsafe {
            frame_extractor::extract_frames(&file_path)
        };

        assert!(result_files_with_frames.is_err());
    }

    #[test]
    fn extract() {
        let file = PathBuf::from("/build/tests/testData/test.mp4");
        let file_path = file.to_str().unwrap();
        let result_files_with_frames = unsafe {
            frame_extractor::extract_frames(&file_path)
        };
        let files_with_frames = result_files_with_frames.unwrap();

        assert!(!files_with_frames.is_empty());
    }
}

