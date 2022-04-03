import React from "react";
import {
  Button,
  ButtonGroup,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Stack,
  Textarea,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";

const Form = ({ onSubmit }) => {
  const {
    register,
    reset,
    setValue,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const handleDirectorySelect = () => {
    window.api.selectFolder().then((result) => {
      if (!!result) {
        console.log(result);
        setValue("directory", result);
      }
    });
  };

  const inputStyles = {
    borderColor: "purple.300",
    focusBorderColor: "purple.400",
    bg: "white",
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={3}>
        <FormControl isInvalid={errors.phrase}>
          <FormLabel htmlFor="phrase">Phrase</FormLabel>
          <Textarea
            id="phrase"
            placeholder="Enter phrase"
            {...register("phrase", {
              required: "Phrase is required",
            })}
            type="text"
            {...inputStyles}
          />
          <FormErrorMessage>
            {errors.phrase && errors.phrase.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={errors.directory}>
          <FormLabel htmlFor="directory">Directory</FormLabel>
          <InputGroup flex flexDirection="column">
            <Input
              id="directory"
              placeholder="Enter directory path"
              {...register("directory", {
                required: "Directory path is required",
              })}
              type="text"
              pr="4.5rem"
              {...inputStyles}
            />
            <FormErrorMessage>
              {errors.directory && errors.directory.message}
            </FormErrorMessage>
            <InputRightElement width="4.5rem">
              <Button size="sm" onClick={handleDirectorySelect}>
                Pick
              </Button>
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <ButtonGroup spacing="6">
          <Button
            mt={4}
            colorScheme="purple"
            isLoading={isSubmitting}
            type="submit"
          >
            Submit
          </Button>

          <Button
            mt={4}
            colorScheme="purple"
            variant="outline"
            onClick={() => reset()}
          >
            Reset form
          </Button>
        </ButtonGroup>
      </Stack>
    </form>
  );
};

export default Form;
