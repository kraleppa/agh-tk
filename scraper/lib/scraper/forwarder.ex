defmodule Scraper.Forwarder do
  require Logger

  alias Scraper.Sender
  alias Scraper.FormatParser

  def run(%{archive_or_video: %{"filePathInVolume" => file_path}, json: json}) do
    Logger.info("Forwarding #{file_path}")

    original_file = Map.get(json, "file")

    Path.extname(file_path)
    |> FormatParser.get_key()
    |> Enum.each(&send(file_path, json, original_file, &1))
  end

  defp send(file_path, json, original_file, key) do
    Map.put(json, "file", file_path)
    |> Map.put("originalFile", original_file)
    |> Sender.send(key)
  end
end
