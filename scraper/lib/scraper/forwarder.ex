defmodule Scraper.Forwarder do
  require Logger

  alias Scraper.Sender
  alias Scraper.FormatParser

  def run(%{archive_or_video: %{"filePathInVolume" => file_path }, json: json} = args) do
    Logger.info("Forwarding #{file_path}")
  end
end
