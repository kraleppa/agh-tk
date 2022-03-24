import { Box, Button, Center, Heading } from "@chakra-ui/react";
import SearchBar from "./Components/SearchBar";
import Data from './data.json'

function App() {
  return (
    <Box bg="gray.600" h="100vh">
      <Center bg="purple.500" h="100px" color="white">
        <Heading>FileFinder</Heading>
      </Center>
      <Center bg="gray.600" h="100px" color="white">
        <Button colorScheme="purple" variant="solid">
          Click me!
        </Button>
      </Center>
      <Center>
        <SearchBar placeholder="Enter your word..." data={Data} />
      </Center>
    </Box>
  );
}

export default App;
