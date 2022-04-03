import React from "react";
import {
  Button,
  ButtonGroup,
  Checkbox,
  CheckboxGroup,
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
    watch,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      phrase: "",
      directory: "",
      synonyms: false,
      typos: false,
      forms: false,
    },
  });

  const watchSynonyms = watch("synonyms", false);
  const watchTypos = watch("typos", false);
  const watchForms = watch("forms", false);

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
                Select
              </Button>
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <FormControl py={0}>
          <FormLabel>Phrase search modes</FormLabel>
          <CheckboxGroup colorScheme="purple">
            <Stack spacing={[2, 6]} direction={["column", "row"]}>
              <Checkbox isChecked={watchSynonyms} {...register("synonyms")}>
                Synonyms
              </Checkbox>
              <Checkbox isChecked={watchTypos} {...register("typos")}>
                Typos
              </Checkbox>
              <Checkbox isChecked={watchForms} {...register("forms")}>
                Various forms
              </Checkbox>
            </Stack>
          </CheckboxGroup>
        </FormControl>

        <ButtonGroup>
          <Stack spacing={[2, 4]} mt={4} direction={["column", "row"]}>
            <Button colorScheme="purple" isLoading={isSubmitting} type="submit">
              Submit
            </Button>
            <Button
              colorScheme="purple"
              variant="outline"
              onClick={() => reset()}
            >
              Reset form
            </Button>
          </Stack>
        </ButtonGroup>
      </Stack>
    </form>
  );
};

export default Form;
