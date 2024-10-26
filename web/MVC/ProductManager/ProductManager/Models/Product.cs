namespace ProductManager.Models
{
    using System;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;

    public class Product
    {
        [Key]
        public int ProductID { get; set; }

        [Required]
        [StringLength(100)]
        public string Name { get; set; }

        [Required]
        public string Category { get; set; }

        [Required]
        public int Quantity { get; set; }

        [ForeignKey("Department")]
        public int? DepartmentID { get; set; }

        public Department Department { get; set; }

        [Required]
        public ProductionStatus ProductionStatus { get; set; }

        [Required]
        public DateTime CreatedDate { get; set; } = DateTime.Now;
    }

    public enum ProductionStatus
    {
        Pending,
        InProgress,
        Completed
    }

}
