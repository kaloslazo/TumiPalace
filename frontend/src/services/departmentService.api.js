import axios from "axios";

const BASE_URL = "http://127.0.0.1:5004/departments";

export const createDepartment = async (department) => {
  const { data } = await axios.post(BASE_URL, department);
  console.log("data: ", data);

  return data;
};