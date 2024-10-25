using System.ComponentModel.DataAnnotations;

namespace TEST2.Models
{
    public class Department
    {
        public int DepartmentID { get; set; }
        [Required]
        public string DepartmentName { get; set; }
    }

}
