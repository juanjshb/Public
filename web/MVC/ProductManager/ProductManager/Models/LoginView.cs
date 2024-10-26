using System.ComponentModel.DataAnnotations;

namespace ProductManager.Models
{
    public class LoginView
    {
        [Required]
        public string Username { get; set; }

        [Required]
        [DataType(DataType.Password)]
        public string Password { get; set; }
    }
}
