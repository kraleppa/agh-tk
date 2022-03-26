import Config

config :scraper,
  queue_name: "words.scraper"

import_config "#{Mix.env()}.exs"
