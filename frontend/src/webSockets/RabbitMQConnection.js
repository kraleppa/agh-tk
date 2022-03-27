import { Stomp } from "@stomp/stompjs";

export class RabbitMQConnection {
  constructor() {
    this.client = Stomp.over(new WebSocket('ws://127.0.0.1:15674/ws'))
    const onConnect = () => console.log('connected to ws')
    const onError = () => console.log('error while connecting to ws')
    this.client.reconnect_delay = 5000
    this.client.connect('guest', 'guest', onConnect, onError)
  }

  sendRequest(phrase, fileTypes, searchModes) {
    const message = createMessage(phrase, fileTypes, searchModes)
    this.client.send('/exchange/words/words.' + getQueueName(searchModes), {}, JSON.stringify(message))
  }

}

function createMessage(phrase, fileTypes, searchModes) {
  return {
    phrase: phrase,
    filters: {
      fileTypes: fileTypes,
      searchModes: searchModes
    }
  }
}

function getQueueName(searchModes) {
  return searchModes.length > 0 ? searchModes[0] : 'scraper'
}