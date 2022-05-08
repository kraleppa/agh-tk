import { Stomp } from "@stomp/stompjs";

export class RabbitMQConnection {
  constructor(addResult) {
    this.client = Stomp.over(new WebSocket("ws://127.0.0.1:15674/ws"));

    const onMessage = (message) => {
      addResult(JSON.parse(message.body));
      this.client.subscribe("/queue/result", onMessage);
    };
    const onConnect = () => {
      console.log("connected to ws");
      this.client.subscribe("/queue/result", onMessage);
    };
    const onError = () => console.error("error while connecting to ws");

    this.client.reconnect_delay = 5000;
    this.client.connect("guest", "guest", onConnect, onError);
  }

  sendRequest(phrase, path, fileTypes, searchModes) {
    searchModes.push("scraper");
    const message = createMessage(phrase, path, fileTypes, searchModes);
    const destination = "/exchange/words/words." + searchModes[0];
    const stringMessage = JSON.stringify(message);
    console.log(
      "Sending message to " + destination + "\n" + "Message: " + stringMessage
    );
    this.client.send(destination, {}, stringMessage);
  }
}

function createMessage(phrase, path, fileTypes, searchModes) {
  return {
    phrase: phrase,
    path: path,
    filters: {
      fileTypes: fileTypes,
      searchModes: searchModes,
    },
    words: phrase.split(" "),
  };
}
