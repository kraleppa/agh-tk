import React from "react";
import { Button, Center, Input } from "@chakra-ui/react";

function SearchBar({ connection, clearResults }) {

  const onClick = () => {
    clearResults()
    // todo replace hardcoded request
    connection.sendRequest('dog', ['docx'], ['forms'])
  }

  return (
    <Center bg="gray.600" h="100px" color="white">
      <Input placeholder="Enter your word..." />
      <Button colorScheme="purple" variant="solid" onClick={onClick}>
        Search
      </Button>
    </Center>
  )
}

export default SearchBar
