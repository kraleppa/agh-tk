import Config

config :scraper,
  queue_name: "words.scraper",
  root_directory: Path.expand("~")

import_config "#{Mix.env()}.exs"
