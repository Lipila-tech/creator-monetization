import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ResetPassword from "@/pages/ResetPassword";
import * as authFirebase from "firebase/auth";

vi.mock("firebase/auth");
vi.mock("react-router-dom", () => ({
  useSearchParams: () => [
    new URLSearchParams("oobCode=validcode123"),
    vi.fn(),
  ],
  useNavigate: () => vi.fn(),
  Link: ({ children, to }) => <a href={to}>{children}</a>,
}));

vi.mock("@/components/Common/MetaTags", () => ({
  default: () => null,
}));

describe("ResetPassword", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(authFirebase.verifyPasswordResetCode).mockResolvedValue("user@example.com");
  });

  it("should verify the reset code on mount", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(authFirebase.verifyPasswordResetCode).toHaveBeenCalled();
    });
  });

  it("should show error for invalid reset code", async () => {
    const mockError = new Error("Invalid code");
    mockError.code = "auth/invalid-action-code";
    vi.mocked(authFirebase.verifyPasswordResetCode).mockRejectedValue(mockError);

    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid reset link/i)).toBeInTheDocument();
    });
  });

  it("should show error for expired reset code", async () => {
    const mockError = new Error("Expired code");
    mockError.code = "auth/expired-action-code";
    vi.mocked(authFirebase.verifyPasswordResetCode).mockRejectedValue(mockError);

    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByText(/reset link has expired/i)).toBeInTheDocument();
    });
  });

  it("should render password form when code is valid", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
      expect(screen.getByLabelText("Confirm Password")).toBeInTheDocument();
    });
  });

  it("should show user email after verification", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByText(/user@example.com/)).toBeInTheDocument();
    });
  });

  it("should show validation error for empty password", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const submitButton = screen.getByText("Reset Password");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Password is required/i)).toBeInTheDocument();
    });
  });

  it("should show validation error for password too short", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const passwordInput = screen.getByLabelText("New Password");
    const submitButton = screen.getByText("Reset Password");
    
    await userEvent.type(passwordInput, "Short1!");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/at least.*8.*characters/i)).toBeInTheDocument();
    });
  });

  it("should show validation error for mismatched passwords", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const passwordInput = screen.getByLabelText("New Password");
    const confirmInput = screen.getByLabelText("Confirm Password");
    const submitButton = screen.getByText("Reset Password");
    
    await userEvent.type(passwordInput, "Password@123");
    await userEvent.type(confirmInput, "DifferentPass@123");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Passwords do not match/i)).toBeInTheDocument();
    });
  });

  it("should call confirmPasswordReset with valid data", async () => {
    const mockConfirm = vi.fn().mockResolvedValue(undefined);
    vi.mocked(authFirebase.confirmPasswordReset).mockImplementation(mockConfirm);

    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const passwordInput = screen.getByLabelText("New Password");
    const confirmInput = screen.getByLabelText("Confirm Password");
    const submitButton = screen.getByText("Reset Password");
    
    await userEvent.type(passwordInput, "ValidPassword@123");
    await userEvent.type(confirmInput, "ValidPassword@123");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockConfirm).toHaveBeenCalledWith(
        expect.any(Object),
        "validcode123",
        "ValidPassword@123"
      );
    });
  });

  it("should show success message after reset", async () => {
    vi.mocked(authFirebase.confirmPasswordReset).mockResolvedValue(undefined);

    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const passwordInput = screen.getByLabelText("New Password");
    const confirmInput = screen.getByLabelText("Confirm Password");
    const submitButton = screen.getByText("Reset Password");
    
    await userEvent.type(passwordInput, "ValidPassword@123");
    await userEvent.type(confirmInput, "ValidPassword@123");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Password reset successfully/i)).toBeInTheDocument();
    });
  });

  it("should toggle password visibility", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const passwordInput = screen.getByLabelText("New Password");
    const showButton = screen.getAllByLabelText(/Show password/i)[0];
    
    expect(passwordInput).toHaveAttribute("type", "password");
    
    await userEvent.click(showButton);
    expect(passwordInput).toHaveAttribute("type", "text");
    
    await userEvent.click(showButton);
    expect(passwordInput).toHaveAttribute("type", "password");
  });

  it("should have proper accessibility attributes", async () => {
    render(<ResetPassword />);
    
    await waitFor(() => {
      const passwordInput = screen.getByLabelText("New Password");
      expect(passwordInput).toHaveAttribute("required");
      
      const confirmInput = screen.getByLabelText("Confirm Password");
      expect(confirmInput).toHaveAttribute("required");
    });
  });

  it("should disable submit button while loading", async () => {
    vi.mocked(authFirebase.confirmPasswordReset).mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<ResetPassword />);
    
    await waitFor(() => {
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    const passwordInput = screen.getByLabelText("New Password");
    const confirmInput = screen.getByLabelText("Confirm Password");
    const submitButton = screen.getByText("Reset Password");
    
    await userEvent.type(passwordInput, "ValidPassword@123");
    await userEvent.type(confirmInput, "ValidPassword@123");
    await userEvent.click(submitButton);
    
    await waitFor(() => {
      expect(submitButton).toBeDisabled();
    });
  });
});
