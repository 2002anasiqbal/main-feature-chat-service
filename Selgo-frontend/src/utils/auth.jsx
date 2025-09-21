import useAuthStore from "../store/authStore";

export const loginUser = (email, password) => {
  const { login } = useAuthStore.getState();
  return login(email, password);
};

export const logoutUser = () => {
  const { logout } = useAuthStore.getState();
  logout();
};
