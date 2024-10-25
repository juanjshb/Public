namespace TEST2.Data
{
    using Microsoft.EntityFrameworkCore;
    using TEST2.Models;

    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Product> Products { get; set; }
        public DbSet<Department> Departments { get; set; }
        public DbSet<User> Users { get; set; }


    }

}
