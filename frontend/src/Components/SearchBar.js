import React from "react";
import { Box, Input, InputGroup, Text } from "@chakra-ui/react";

function SearchBar() {
  return (
    <Box>
      <Text mb="8px" color="white">
        Phrase
      </Text>
      <InputGroup flex flexDirection="column">
        <Input
          placeholder="Enter phrase"
          bg="white"
          focusBorderColor="purple.400"
          borderColor="purple.300"
        />
      </InputGroup>
    </Box>
  );
}

export default SearchBar;
