import { Box, Badge, Flex, Heading, Grid, GridItem } from "@chakra-ui/react";
import { fileFormats } from "./file-formats";

const Result = ({ path, fileFormat }) => {
  const badgeBackgroundColor = fileFormats.find(
    (format) => format.value === fileFormat
  )?.color;

  return (
    <Grid templateColumns="repeat(12, 1fr)" gap={4}>
      <GridItem colSpan={11}>
        <Box py="4">
          <Heading size="sm">{path}</Heading>
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
