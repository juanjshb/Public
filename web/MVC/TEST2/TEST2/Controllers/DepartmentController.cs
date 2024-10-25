using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TEST2.Data;

namespace TEST2.Controllers
{
    ///[Authorize(Policy = "UserPolicy,AdminPolicy")]
    public class DepartmentController : Controller
    {
        private readonly ApplicationDbContext _context;

        public DepartmentController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: Departments
        public async Task<IActionResult> Index(int? departmentId, string departmentName)
        {
            var departments = _context.Departments.AsQueryable();

            // Implement filtering logic here based on parameters if needed.
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
