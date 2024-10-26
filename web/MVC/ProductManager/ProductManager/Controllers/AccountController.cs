using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProductManager.Data;
using ProductManager.Models;
using ProductManager.Utils;
using System.Diagnostics;
using System.Security.Claims;

namespace ProductManager.Controllers
{
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
                return View(model); // Return the view with errors if the model is invalid.
            }

            // Hash the incoming password to compare it with the stored password hash.
            var hashPassword = new PasswordEncrypter().HashPassword(model.Password);

            // Fetch the user from the database based on the username and hashed password.
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == model.Username && u.PasswordHash == hashPassword);

            // If the user is not found, add an error and return the view.
            if (user == null)
            {
                return RedirectToAction("Index", "Product");
                ModelState.AddModelError("", "Invalid Username or Password.");
                return View(model); // Return the view with the model to display validation errors.
            }

            // If the user is found, create claims for authentication.
            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Role, user.Role.ToString())
            };

            var claimsIdentity = new ClaimsIdentity(claims, "CookieAuth");
            var claimsPrincipal = new ClaimsPrincipal(claimsIdentity);

            // Sign in the user.
            await HttpContext.SignInAsync("CookieAuth", claimsPrincipal);

            // Redirect to the Index action of the Product controller upon successful login.
            return RedirectToAction("Index", "Product");
        }

    }
}
