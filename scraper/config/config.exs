import Config

config :scraper,
  queue_name: "words.scraper"


config :amqp,
  channels: [
    receiver: [connection: :myconn],
    sender: [connection: :myconn]
  ]

import_config "#{Mix.env()}.exs"
