export const isArchivePath = (path) => {
  const archiveTypes = ["zip", "tar", "gz"];
  return archiveTypes.includes(path.split(".").pop());
};
