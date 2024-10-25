using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;
using TEST2.Data;
using TEST2.Models;
using TEST2.Utils;

public class AccountController : Controller
{
    private readonly ApplicationDbContext _context;

    public AccountController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public IActionResult Login()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Login(LoginView model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        // Hash the password input from the user
        var hashedPassword = PasswordHelper.HashPassword(model.Password);

        // Validate user credentials with hashed password
        var user = _context.Users
            .FirstOrDefault(u => u.Username == model.Username && u.PasswordHash == hashedPassword);

        if (user == null)
        {
            ModelState.AddModelError("", "Invalid username or password.");
            return View(model);
        }

        // Create user claims and authenticate as before
        var claims = new List<Claim>
    {
        new Claim(ClaimTypes.Name, user.Username),
        new Claim(ClaimTypes.Role, user.Role.ToString())
    };

        var claimsIdentity = new ClaimsIdentity(claims, "CookieAuth");
        var claimsPrincipal = new ClaimsPrincipal(claimsIdentity);

        await HttpContext.SignInAsync("CookieAuth", claimsPrincipal);

        return RedirectToAction("Index", "Home");
    }


    [HttpPost]
    public async Task<IActionResult> Logout()
    {
        await HttpContext.SignOutAsync("CookieAuth");
        return RedirectToAction("Login", "Account");
    }
}
