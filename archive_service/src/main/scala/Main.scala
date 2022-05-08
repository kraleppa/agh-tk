import scala.language.postfixOps
import consumer.Consumer

object Main {
  def main(args: Array[String]): Unit = {
    new Consumer().run()
  }
}
