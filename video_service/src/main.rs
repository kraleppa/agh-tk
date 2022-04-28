use std::env;
use amiquip::{Connection, ConsumerMessage, ConsumerOptions, Publish, Result};
use log::LevelFilter;

#[macro_use]
extern crate log;
extern crate env_logger;

mod frameExtractor;

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
                let result_files_with_frames = frameExtractor::extract_frames(file);
                if result_files_with_frames.is_err() {
                    error!("no frames extracted {:?}", result_files_with_frames.err());
                    consumer.ack(delivery)?;
                    continue;
                }

                let files_with_frames = result_files_with_frames.unwrap();
                for file in files_with_frames.iter() {
                    let mut to_send = v.clone();
                    let mut map = Map::new();
                    map.insert("framePath".to_string(), Value::String(file));
                    to_send["video"] = Value::Object(map);
                    let mut msg_to_send = to_send.to_string();
                    info!("Sending: {}", msg_to_send);
                    channel.basic_publish("words",Publish::new(msg_to_send.as_bytes(),"words.scraper"));
                }

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