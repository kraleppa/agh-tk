use std::env;
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

    let mut connection = Connection::insecure_open(&rabit_connection)?;
    let channel = connection.open_channel(None)?;
    channel.queue_bind("format.movie", "format", "format.movie.*", Default::default())?;

    let consumer = channel.basic_consume("format.movie", ConsumerOptions::default())?;

    info!("Consumer loop starting");
    for (_, message) in consumer.receiver().iter().enumerate() {
        match message {
            ConsumerMessage::Delivery(delivery) => unsafe {
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
                    consumer.ack(delivery)?;
                    continue;
                }

                let file = file_option.unwrap();
                info!("file: {}", file);
                let result_files_with_frames = frame_extractor::extract_frames(file);
                if result_files_with_frames.is_err() {
                    error!("no frames extracted {:?}", result_files_with_frames.err());
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

pub fn send_json_with_frames(channel: &Channel, files_with_frames: &Vector<String>, value: &Value) {
    for file in files_with_frames.iter() {
        let mut to_send = value.clone();
        let mut map = Map::new();
        map.insert("framePath".to_string(), Value::String(file));
        to_send["video"] = Value::Object(map);
        let mut msg_to_send = to_send.to_string();
        info!("Sending : {}", msg_to_send);
        channel.basic_publish("words", Publish::new(msg_to_send.as_bytes(), "words.scraper"));
    }

}



#[cfg(test)]
mod extractor_test{
    use std::path::{PathBuf};
    use crate::frame_extractor;

    #[test]
    #[should_panic]
    fn failed_extract(){
        let file = PathBuf::from("/non/existing/path/test.mp4");
        let file_path = file.to_str().unwrap();
        println!("{}", file_path);
        let result_files_with_frames = unsafe {
            frame_extractor::extract_frames(&file_path)
        };

        assert!(result_files_with_frames.is_err());
    }

    #[test]
    fn extract(){

        let file = PathBuf::from("/build/tests/testData/test.mp4");
        let file_path = file.to_str().unwrap();
        println!("{}", file_path);
        let result_files_with_frames = unsafe {
            frame_extractor::extract_frames(&file_path)
        };
        let files_with_frames = result_files_with_frames.unwrap();
        println!("{:?}", files_with_frames);
        assert!(!files_with_frames.is_empty());
    }

}

