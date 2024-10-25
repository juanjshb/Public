using System.ComponentModel.DataAnnotations;

namespace TEST2.Models
{
    public class Product
    {
        public int ProductID { get; set; }
        [Required]
        public string Name { get; set; }
        [Required]
        public string Category { get; set; }
        [Required]
        public int Quantity { get; set; }
        public int? DepartmentID { get; set; }
        public ProductionStatus ProductionStatus { get; set; }
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public virtual Department Department { get; set; }
    }

    public enum ProductionStatus
    {
        Pending,
        InProgress,
        Completed
    }
}
