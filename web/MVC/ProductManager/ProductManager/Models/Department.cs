namespace ProductManager.Models
{
    using System.ComponentModel.DataAnnotations;

    public class Department
    {
        [Key]
        public int DepartmentID { get; set; }

        [Required]
        [StringLength(100)]
        public string DepartmentName { get; set; }
    }

}
