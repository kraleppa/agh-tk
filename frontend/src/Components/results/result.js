import { Box, Badge, Flex, Heading, Grid, GridItem } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { fileFormats } from "./file-formats";

const Result = ({ path, fileFormat, fileState }) => {
  const badgeBackgroundColor = fileFormats.find(
    (format) => format.value === fileFormat
  )?.color;

  const [parsedFileState, setParsedFileState] = useState("");

  useEffect(() => {
    setParsedFileState(parseFileState(fileState));
  }, [fileState]);

  const parseFileState = (fileState) => {
    if (!fileState) {
      return "";
    } else if (fileState.textFound != null) {
      if (!!fileState.textFound) {
        return "Text found";
      } else {
        return "Text not found";
      }
    } else if (!!fileState.fileFound) {
      return "Processing...";
    } else {
      return "Text not found";
    }
  };

  return (
    <Grid templateColumns="repeat(12, 1fr)" gap={4}>
      <GridItem colSpan={8}>
        <Box py="4">
          <Heading size="sm">{path}</Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={3}>
        <Box py="4">
          <Heading size="sm">{parsedFileState}</Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={1}>
        <Flex height="100%" alignItems="center" justifyContent="flex-end">
          <Badge background={badgeBackgroundColor}>{fileFormat}</Badge>
        </Flex>
      </GridItem>
    </Grid>
  );
};

export default Result;
