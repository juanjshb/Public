using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TEST2.Data;
using TEST2.Models;

namespace TEST2.Controllers
{
    ///[Authorize(Policy = "AdminPolicy")]
    public class ProductController : Controller
    {
        private readonly ApplicationDbContext _context;

        public ProductController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: Products
        public async Task<IActionResult> Index(string category, ProductionStatus? status, int? departmentId)
        {
            var products = _context.Products.Include(p => p.Department).AsQueryable();

            // Implement filtering logic here based on parameters.

            return View(await products.ToListAsync());
        }

    }
}
