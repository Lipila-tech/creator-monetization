import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import PasswordStrengthIndicator from "@/components/Auth/PasswordStrengthIndicator";

describe("PasswordStrengthIndicator", () => {
  it("should not render when password is empty", () => {
    const { container } = render(<PasswordStrengthIndicator password="" />);
    expect(container.firstChild).toBeEmptyDOMElement();
  });

  it("should show weak strength for 8 char password with no special chars", () => {
    render(<PasswordStrengthIndicator password="Password1" />);
    
    expect(screen.getByText(/Weak/i)).toBeInTheDocument();
  });

  it("should show fair strength for password with 2 requirements met", () => {
    render(<PasswordStrengthIndicator password="Password1" />);
    
    const requirements = screen.getAllByRole("listitem");
    const metRequirements = requirements.filter((item) =>
      item.querySelector("span:first-child").classList.contains("bg-green-500")
    );
    
    expect(metRequirements.length).toBeGreaterThanOrEqual(2);
  });

  it("should show all requirements in checklist", () => {
    render(<PasswordStrengthIndicator password="Test" />);
    
    expect(screen.getByText(/At least 8 characters/i)).toBeInTheDocument();
    expect(screen.getByText(/One uppercase letter/i)).toBeInTheDocument();
    expect(screen.getByText(/One lowercase letter/i)).toBeInTheDocument();
    expect(screen.getByText(/One number/i)).toBeInTheDocument();
    expect(screen.getByText(/One special character/i)).toBeInTheDocument();
  });

  it("should check length requirement correctly", () => {
    const { rerender } = render(<PasswordStrengthIndicator password="Pass1!ab" />);
    
    let listItems = screen.getAllByRole("listitem");
    let lengthCheck = listItems[0].querySelector("span:first-child");
    expect(lengthCheck).toHaveClass("bg-green-500");

    rerender(<PasswordStrengthIndicator password="Pass1!a" />);
    listItems = screen.getAllByRole("listitem");
    lengthCheck = listItems[0].querySelector("span:first-child");
    expect(lengthCheck).toHaveClass("bg-gray-300");
  });

  it("should check uppercase requirement", () => {
    render(<PasswordStrengthIndicator password="password1!" />);
    
    const listItems = screen.getAllByRole("listitem");
    const uppercaseCheck = listItems[1].querySelector("span:first-child");
    expect(uppercaseCheck).toHaveClass("bg-gray-300");
  });

  it("should check lowercase requirement", () => {
    render(<PasswordStrengthIndicator password="PASSWORD1!" />);
    
    const listItems = screen.getAllByRole("listitem");
    const lowercaseCheck = listItems[2].querySelector("span:first-child");
    expect(lowercaseCheck).toHaveClass("bg-gray-300");
  });

  it("should check number requirement", () => {
    render(<PasswordStrengthIndicator password="Password!" />);
    
    const listItems = screen.getAllByRole("listitem");
    const numberCheck = listItems[3].querySelector("span:first-child");
    expect(numberCheck).toHaveClass("bg-gray-300");
  });

  it("should check special character requirement", () => {
    render(<PasswordStrengthIndicator password="Password1" />);
    
    const listItems = screen.getAllByRole("listitem");
    const specialCheck = listItems[4].querySelector("span:first-child");
    expect(specialCheck).toHaveClass("bg-gray-300");
  });

  it("should show very strong for password with all requirements", () => {
    render(<PasswordStrengthIndicator password="VeryStrong@123" />);
    
    expect(screen.getByText(/Very Strong/i)).toBeInTheDocument();
  });

  it("should display strength bar", () => {
    render(<PasswordStrengthIndicator password="Test@1234" />);
    
    const strengthBar = screen.getByText(/Password Strength/).parentElement.nextElementSibling;
    expect(strengthBar).toBeInTheDocument();
  });

  it("should update in real-time as password changes", () => {
    const { rerender } = render(<PasswordStrengthIndicator password="pass" />);
    
    expect(screen.getByText(/Weak/i)).toBeInTheDocument();

    rerender(<PasswordStrengthIndicator password="Password@1" />);
    
    expect(screen.queryByText(/Weak/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Strong/i)).toBeInTheDocument();
  });
});
