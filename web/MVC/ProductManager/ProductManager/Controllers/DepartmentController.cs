using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProductManager.Data;
using ProductManager.Models;

namespace ProductManager.Controllers
{
    public class DepartmentController : Controller
    {

        private readonly ApplicationDbContext _context;

        public DepartmentController(ApplicationDbContext context)
        {
            _context = context;
        }

        //Get departments
        public async Task<IActionResult> Index(int? departmentId, string departmentName)
        {
            var departments = _context.Departments.AsQueryable();


            if (departmentId.HasValue) 
            {
                departments = departments.Where(d => d.DepartmentID == departmentId.Value);
            }

            if (!string.IsNullOrEmpty(departmentName))
            {
                departments = departments.Where(d => d.DepartmentName.Contains(departmentName));
            }

            return View(await departments.ToListAsync());
        }
    }
}
