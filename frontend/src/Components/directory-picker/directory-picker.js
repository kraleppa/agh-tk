import {
  Box,
  Button,
  Input,
  InputGroup,
  InputRightElement,
} from "@chakra-ui/react";
import { useState } from "react";
import { AiOutlineFolderOpen } from "react-icons/ai";

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
    <InputGroup>
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
          <Box as={AiOutlineFolderOpen} size="24px" />
        </Button>
      </InputRightElement>
    </InputGroup>
  );
};

export default DirectoryPicker;
