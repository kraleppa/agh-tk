import Config

config :scraper,
  queue_name: "words.scraper",
  root_directory: ""

import_config "#{Mix.env()}.exs"
