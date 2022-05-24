package pl.agh.tk.odt;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Consumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

//TODO: add this everywhere
public class Main {

    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) throws InterruptedException, IOException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("rabbitmq");

        Connection connection = null;

        while(connection == null) {
            try{
                connection = connectionFactory.newConnection();
            }
            catch(IOException | TimeoutException e){
                logger.warn("waiting for connection");
                Thread.sleep(10_000);
            }
        }

        Channel channelIn = connection.createChannel();
        Channel channelOut = connection.createChannel();
        Consumer consumer = new OdtConsumer(channelIn, channelOut);

        channelIn.basicConsume("format.opendoc", true, consumer);


    }

}
