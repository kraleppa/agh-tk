import Config

config :scraper,
  queue_name: "words.scraper",
  exchange_name: "format"


config :amqp,
  channels: [
    receiver: [connection: :myconn],
    sender: [connection: :myconn]
  ]

import_config "#{Mix.env()}.exs"
