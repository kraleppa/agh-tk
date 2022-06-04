import amqp from 'amqplib'
import translate from 'translate-google'

const connection = await amqp.connect('amqp://rabbitmq')
const channel = await connection.createChannel()
await channel.assertQueue('words.translations', { durable: true })

function shiftLeft(array) {
    const [head, ...tail] = array
    return [...tail, head]
}

channel.consume('words.translations', async message => {
    const request = JSON.parse(message.content.toString())
    const languages = request.languages ?? []
    const translations = await Promise.all(languages.map(lang => translate(request.phrase, { from: 'pl', to: lang })))
    request.words.push(...translations)

    console.log(`translations for ${request.phrase}: ${translations}`)
    const [next,] = request.filters.searchModes = shiftLeft(request.filters.searchModes)
    const routingKey = `words.${next}`
    channel.publish('words', routingKey, Buffer.from(JSON.stringify(request), 'utf8'))
    channel.ack(message)
})