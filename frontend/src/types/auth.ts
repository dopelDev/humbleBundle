export interface UserInfo {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserInfo;
}

export interface LoginPayload {
  username: string;
  password: string;
}

