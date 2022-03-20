import Config

config :amqp,
  connections: [
    myconn: [
      host: "rabbitmq",
      port: 5672,
      virtual_host: "/",
      username: "guest",
      password: "guest"
    ],
  ],
  channels: [
    mychan: [connection: :myconn]
  ]
