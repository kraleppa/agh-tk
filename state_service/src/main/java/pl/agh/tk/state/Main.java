package pl.agh.tk.state;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import static pl.agh.tk.state.Utils.HOST;
import static pl.agh.tk.state.Utils.QUEUE_NAME;

public class Main {

    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) throws InterruptedException, IOException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost(HOST);
        Connection connection = null;

        while (connection == null) {
            try {
                connection = connectionFactory.newConnection();
            } catch (IOException | TimeoutException e) {
                logger.info("Waiting for connection");
                Thread.sleep(10_000);
            }
        }
        logger.info("Connected successfully");

        Channel channel = connection.createChannel();

        StateConsumer consumer = new StateConsumer(channel);
        channel.basicConsume(QUEUE_NAME, consumer);
    }
}
