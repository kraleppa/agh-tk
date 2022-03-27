import Config

config :amqp,
  connections: [
    myconn: [
      host: "localhost",
      port: 5672,
      virtual_host: "/",
      username: "guest",
      password: "guest"
    ]
  ]

config :scraper,
  env: :dev
