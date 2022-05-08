import Config

config :scraper,
  queue_name: "words.scraper",
  exchange_name: "format",
  info_exchange: "result"

config :amqp,
  channels: [
    receiver: [connection: :myconn],
    sender: [connection: :myconn]
  ]

import_config "#{Mix.env()}.exs"
