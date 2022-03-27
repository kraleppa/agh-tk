import { Box, Center, Container, Heading } from "@chakra-ui/react";
import SearchBar from "./Components/SearchBar";
import data from "./data.json";
import { RabbitMQConnection } from "./webSockets/RabbitMQConnection";
import { useEffect, useState } from "react";
import ShowResults from "./Components/ShowResults";
import DirectoryPicker from "./Components/directory-picker/directory-picker";

function App() {
  const [results, setResults] = useState(data);
  const clearResults = () => setResults([]);
  const addResult = (newResult) => {
    console.log("adding result: " + JSON.stringify(newResult));
    setResults((oldResults) => [...oldResults, newResult]);
  };

  const connection = new RabbitMQConnection(addResult);

  useEffect(() => {
    console.dir(results);
  }, [results]);

  return (
    <Box bg="gray.600" h="100vh">
      <Container maxW="container.xl">
        <Center bg="purple.500" h="100px" color="white">
          <Heading>FileFinder</Heading>
        </Center>
        <Center>
          <SearchBar connection={connection} clearResults={clearResults} />
        </Center>
        <DirectoryPicker />
        <Center>
          <ShowResults results={results} />
        </Center>
      </Container>
    </Box>
  );
}

export default App;
