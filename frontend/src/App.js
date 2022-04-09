import { Box, Container, Heading, SimpleGrid } from "@chakra-ui/react";
import { RabbitMQConnection } from "./webSockets/RabbitMQConnection";
import { useEffect, useState } from "react";
import Results from "./Components/results/results";
import Form from "./Components/form/form";

function App() {
  const [results, setResults] = useState([]);
  const clearResults = () => setResults([]);
  const addResult = (newResult) => {
    console.log("adding result: " + JSON.stringify(newResult));
    setResults((oldResults) => [...oldResults, newResult]);
  };

  const connection = new RabbitMQConnection(addResult);

  const onSubmit = ({ phrase, path }, fileFormats, searchModes) => {
    clearResults();
    connection.sendRequest(
      phrase,
      path.replace(/\\/g, "/"),
      [...fileFormats],
      [...searchModes]
    );
  };

  useEffect(() => {
    console.dir(results);
  }, [results]);

  return (
    <Box minHeight={"100vh"} bg="gray.50" mb="5">
      <Container
        bg="gray.50"
        minHeight={"100vh"}
        py={6}
        px={6}
        maxW="container.lg"
      >
        <SimpleGrid columns={1} spacing={5}>
          <Box py={4} h="80px" color="purple.500">
            <Heading>FileFinder</Heading>
          </Box>
          <Form onSubmit={onSubmit} />
          <Results results={results} />
        </SimpleGrid>
      </Container>
    </Box>
  );
}

export default App;
