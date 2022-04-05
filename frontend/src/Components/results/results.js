import { Box, Divider, Flex, Grid, GridItem, Heading } from "@chakra-ui/react";
import Result from "./result";

const Results = ({ results }) => {
  console.log(results);
  return (
    <Box mt={8} borderRadius="5px">
      <Heading size="lg" mb={6}>
        Results
      </Heading>

      <Grid templateColumns="repeat(12, 1fr)" gap={4}>
        <GridItem colSpan={11}>
          <Box py="4">
            <Heading size="sm">Path</Heading>
          </Box>
        </GridItem>
        <GridItem colSpan={1}>
          <Flex height="100%" alignItems="center" justifyContent="flex-end">
            <Heading size="sm">Format</Heading>
          </Flex>
        </GridItem>
      </Grid>

      <Divider borderColor="gray.300" />

      {results.map((result, i) => (
        <>
          <Result
            path={result.path}
            fileFormat={result.path.split(".").pop()}
          ></Result>
          {i < results.length - 1 ? <Divider borderColor="gray.300" /> : null}
        </>
      ))}
    </Box>
  );
};

export default Results;
