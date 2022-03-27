import {
  Box,
  Button,
  Input,
  InputGroup,
  InputRightElement,
  Text,
} from "@chakra-ui/react";
import { useState } from "react";

const DirectoryPicker = () => {
  const [directoryPath, setDirectoryPath] = useState("");

  const handleChange = (event) => setDirectoryPath(event.target.value);

  const handleClick = () => {
    window.api.selectFolder().then((result) => {
      if (!!result) {
        setDirectoryPath(result);
      }
    });
  };

  return (
    <Box>
      <Text color="white" mb="8px">
        Directory
      </Text>
      <InputGroup flex flexDirection="column">
        <Input
          value={directoryPath}
          onChange={handleChange}
          type="text"
          pr="4.5rem"
          placeholder="Enter directory path"
          bg="white"
          focusBorderColor="purple.400"
          borderColor="purple.300"
        />
        <InputRightElement width="4.5rem">
          <Button size="sm" onClick={handleClick}>
            Pick
          </Button>
        </InputRightElement>
      </InputGroup>
    </Box>
  );
};

export default DirectoryPicker;
