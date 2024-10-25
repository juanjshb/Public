using System.ComponentModel.DataAnnotations;

namespace TEST2.Models
{
    public class User
    {
        public int UserID { get; set; }
        [Required]
        public string Username { get; set; }
        [Required]
        public string PasswordHash { get; set; }
        public UserRole Role { get; set; }
    }

    public enum UserRole
    {
        Admin,
        User
    }

}
