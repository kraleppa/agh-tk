export const isArchivePath = (path) => {
  const archiveTypes = ["zip", "tar", "gz"];
  return archiveTypes.includes(path.split(".").pop());
};

export const sendRequest = (client, phrase, path, fileTypes, searchModes) => {
  const message = {
    phrase: phrase,
    path: path.replace(/\\/g, "/"),
    filters: {
      fileTypes: fileTypes,
      searchModes: [...searchModes, "scraper"],
    },
    words: phrase.split(" "),
  };

  const destination = "/exchange/words/words." + message.filters.searchModes[0];
  const stringMessage = JSON.stringify(message);

  console.info("Sending message: " + stringMessage);

  client.publish({
    destination: destination,
    body: stringMessage,
    headers: {},
  });
};
