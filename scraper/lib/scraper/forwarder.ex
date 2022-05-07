defmodule Scraper.Forwarder do
  require Logger

  alias Scraper.Sender
  alias Scraper.FormatParser

  def run(%{archive_or_video: %{"filePathInVolume" => file_path}, json: json}) do
    Logger.info("Forwarding #{file_path}")

    key =
      Path.extname(file_path)
      |> FormatParser.get_key()

    original_file = Map.get(json, "file")

    Map.put(json, "file", file_path)
      |> Map.put("originalFile", original_file)
      |> Sender.send(key)
  end
end
