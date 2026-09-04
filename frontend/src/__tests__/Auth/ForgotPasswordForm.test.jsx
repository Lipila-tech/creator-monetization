import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ForgotPasswordForm from "@/components/Auth/ForgotPasswordForm";
import * as authFirebase from "firebase/auth";

vi.mock("firebase/auth");
vi.mock("react-router-dom", () => ({
  Link: ({ children, to }) => <a href={to}>{children}</a>,
}));

describe("ForgotPasswordForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should render the form with email input", () => {
    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    expect(emailInput).toBeInTheDocument();
    expect(screen.getByText("Send Reset Link")).toBeInTheDocument();
  });

  it("should show validation error for empty email", async () => {
    render(<ForgotPasswordForm />);
    
    const submitButton = screen.getByText("Send Reset Link");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText("Email address is required.")).toBeInTheDocument();
    });
  });

  it("should show validation error for invalid email", async () => {
    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    await userEvent.type(emailInput, "invalidemail");
    
    await waitFor(() => {
      expect(screen.getByText("Please enter a valid email address.")).toBeInTheDocument();
    });
  });

  it("should accept valid email format", async () => {
    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    await userEvent.type(emailInput, "user@example.com");
    
    await waitFor(() => {
      expect(screen.queryByText("Please enter a valid email address.")).not.toBeInTheDocument();
    });
  });

  it("should call sendPasswordResetEmail with valid email", async () => {
    const mockSendEmail = vi.fn().mockResolvedValue(undefined);
    vi.mocked(authFirebase.sendPasswordResetEmail).mockImplementation(mockSendEmail);

    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    const submitButton = screen.getByText("Send Reset Link");
    
    await userEvent.type(emailInput, "user@example.com");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockSendEmail).toHaveBeenCalledWith(expect.any(Object), "user@example.com");
    });
  });

  it("should show success message on successful email send", async () => {
    vi.mocked(authFirebase.sendPasswordResetEmail).mockResolvedValue(undefined);

    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    const submitButton = screen.getByText("Send Reset Link");
    
    await userEvent.type(emailInput, "user@example.com");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Password reset email sent!/i)).toBeInTheDocument();
    });
  });

  it("should handle rate limiting error", async () => {
    const mockError = new Error("Too many requests");
    mockError.code = "auth/too-many-requests";
    vi.mocked(authFirebase.sendPasswordResetEmail).mockRejectedValue(mockError);

    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    const submitButton = screen.getByText("Send Reset Link");
    
    await userEvent.type(emailInput, "user@example.com");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Too many reset attempts/i)).toBeInTheDocument();
    });
  });

  it("should handle invalid email error from Firebase", async () => {
    const mockError = new Error("Invalid email");
    mockError.code = "auth/invalid-email";
    vi.mocked(authFirebase.sendPasswordResetEmail).mockRejectedValue(mockError);

    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByPlaceholderText("you@example.com");
    const submitButton = screen.getByText("Send Reset Link");
    
    await userEvent.type(emailInput, "user@example.com");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText("Please enter a valid email address.")).toBeInTheDocument();
    });
  });

  it("should have proper accessibility attributes", () => {
    render(<ForgotPasswordForm />);
    
    const emailInput = screen.getByLabelText("Email Address");
    expect(emailInput).toHaveAttribute("required");
    expect(emailInput).toHaveAttribute("autoComplete", "email");
    
    const submitButton = screen.getByRole("button", { name: /Send Reset Link/i });
    expect(submitButton).toBeInTheDocument();
  });

  it("should show helpful tip about spam folder", () => {
    render(<ForgotPasswordForm />);
    
    expect(screen.getByText(/Check your spam folder/i)).toBeInTheDocument();
    expect(screen.getByText(/reset link expires in 1 hour/i)).toBeInTheDocument();
  });
});
